================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Queen Margrethe II


Countess Athena of Monpezat (born Athena Marguerite Françoise Marie; 24 January 2012) is a member of the Danish royal family.
She is the younger child and only daughter of Prince Joachim and Princess Marie of Denmark.
She is the youngest grandchild of Queen Margrethe II and Prince Henrik, and the niece of King Frederik X. Athena is currently ninth in the line of succession to the Danish throne.
Biography

Athena was born a princess of Denmark on 24 January 2012 at Rigshospitalet, the Copenhagen University Hospital.
She has two older half-brothers from her father's first marriage, Nikolai and Felix, and an older brother, Henrik.
In accordance with Danish royal traditions, her names were not revealed until her christening, which took place on 20 May 2012 at the Møgeltønder Church, where her older brothers Felix and Henrik were also christened.
She was named Athena Marguerite Françoise Marie for both of her grandmothers as well as for her mother.
Her godparents are her maternal uncles, Gregory Grandet and Edouard Cavallier; Carina Axelsson, the long-term girlfriend of her father's cousin Gustav, Hereditary Prince of Sayn-Wittgenstein-Berleburg; and friends of her parents, Julie Mirabaud, Diego de Lavandeyra and Henriette Steenstrup.
Joseph Søstrenes Skole – the same Catholic private school in Ordrup as her brother Henrik.
In 2019, when Athena and her family moved to France, she was enrolled at the private school EIB Monceau in the 8th arrondissement of Paris alongside her brother.
Titles and styles

Athena was styled as "Her Highness Princess Athena of Denmark, Countess of Monpezat" from birth until 1 January 2023.
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
Since 1 January 2023, she has been known as "Her Excellency Countess Athena of Monpezat".



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b87253ed-6240-49f5-b9ea-c5a1e57ea861)
 Call ID: b87253ed-6240-49f5-b9ea-c5a1e57ea861
  Args:
    source: Athena_of_Monpezat
    type: :Woman
  AssignClass (a52e8323-b48d-41ba-88c6-6d3282d67a8c)
 Call ID: a52e8323-b48d-41ba-88c6-6d3282d67a8c
  Args:
    source: Athena_of_Monpezat
    type: :Person
  AddLiteral (0149c2ae-d774-4f38-8d5f-47dc7722b8b3)
 Call ID: 0149c2ae-d774-4f38-8d5f-47dc7722b8b3
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: Athena_of_Monpezat
    literal_value: Athena Marguerite Françoise Marie
  AddLiteral (da48c7f7-a11f-40ea-b054-286e5c23f1e1)
 Call ID: da48c7f7-a11f-40ea-b054-286e5c23f1e1
  Args:
    literal_value: 2012
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Athena_of_Monpezat
  AssignClass (635d12fc-4879-4b06-9000-e016bbc17c87)
 Call ID: 635d12fc-4879-4b06-9000-e016bbc17c87
  Args:
    source: Prince_Joachim
    type: :Man
  AssignClass (f2e88f89-8538-4213-a7e8-5e4bcfe9d570)
 Call ID: f2e88f89-8538-4213-a7e8-5e4bcfe9d570
  Args:
    source: Prince_Joachim
    type: :Person
  AssignClass (05055ed3-021d-43a2-88d7-bcec1400ba17)
 Call ID: 05055ed3-021d-43a2-88d7-bcec1400ba17
  Args:
    source: Princess_Marie_of_Denmark
    type: :Woman
  AssignClass (33cc91cd-a4b0-4a36-a226-54a8a3d2de3a)
 Call ID: 33cc91cd-a4b0-4a36-a226-54a8a3d2de3a
  Args:
    source: Princess_Marie_of_Denmark
    type: :Person
  AddTriple (f51642d0-2b33-4fbf-8398-d45ca972a2ed)
 Call ID: f51642d0-2b33-4fbf-8398-d45ca972a2ed
  Args:
    target: Prince_Joachim
    relation: :hasFather
    source: Athena_of_Monpezat
  AddTriple (6871f069-85b7-4609-89e4-27bed9232713)
 Call ID: 6871f069-85b7-4609-89e4-27bed9232713
  Args:
    source: Athena_of_Monpezat
    relation: :hasMother
    target: Princess_Marie_of_Denmark
  AssignClass (34f2acc8-c700-49f0-8355-39d9931651d1)
 Call ID: 34f2acc8-c700-49f0-8355-39d9931651d1
  Args:
    source: Queen_Margrethe_II
    type: :Woman
  AssignClass (251267c9-4df1-4295-a962-0f959b8e8343)
 Call ID: 251267c9-4df1-4295-a962-0f959b8e8343
  Args:
    source: Queen_Margrethe_II
    type: :Person
  AssignClass (bcb6a99d-7a1e-4d11-8cbd-fbcabf3e35fd)
 Call ID: bcb6a99d-7a1e-4d11-8cbd-fbcabf3e35fd
  Args:
    source: Prince_Henrik
    type: :Man
  AssignClass (60f9b8a7-50a2-4565-af2e-01a68a8b4eff)
 Call ID: 60f9b8a7-50a2-4565-af2e-01a68a8b4eff
  Args:
    source: Prince_Henrik
    type: :Person
  AddTriple (fde768fe-a2ec-4918-8d5a-f719c89bf307)
 Call ID: fde768fe-a2ec-4918-8d5a-f719c89bf307
  Args:
    target: Queen_Margrethe_II
    source: Prince_Joachim
    relation: :hasParent
  AddTriple (19fff6a3-6ad0-492e-90de-2c8f23970740)
 Call ID: 19fff6a3-6ad0-492e-90de-2c8f23970740
  Args:
    target: Prince_Henrik
    relation: :hasParent
    source: Prince_Joachim
  AssignClass (ea77876f-f648-4400-9c2c-223e5cb8576d)
 Call ID: ea77876f-f648-4400-9c2c-223e5cb8576d
  Args:
    source: King_Frederik_X
    type: :Man
  AssignClass (fc68fa95-0772-4c8e-b385-2d885d6ce47a)
 Call ID: fc68fa95-0772-4c8e-b385-2d885d6ce47a
  Args:
    source: King_Frederik_X
    type: :Person
  AssignClass (3cd872f5-f153-4f21-bff9-8a16b9deec28)
 Call ID: 3cd872f5-f153-4f21-bff9-8a16b9deec28
  Args:
    source: Nikolai
    type: :Man
  AssignClass (d83f696e-89bb-4acd-ac45-246f0799942c)
 Call ID: d83f696e-89bb-4acd-ac45-246f0799942c
  Args:
    source: Nikolai
    type: :Person
  AssignClass (d78a1742-23b1-4bd9-9604-4cfa10885260)
 Call ID: d78a1742-23b1-4bd9-9604-4cfa10885260
  Args:
    source: Felix
    type: :Man
  AssignClass (97070a9a-04ba-4c1b-8d24-6037cc4b23a4)
 Call ID: 97070a9a-04ba-4c1b-8d24-6037cc4b23a4
  Args:
    source: Felix
    type: :Person
  AssignClass (f8e1b9b7-3cce-49a0-92fc-b0de6bb55833)
 Call ID: f8e1b9b7-3cce-49a0-92fc-b0de6bb55833
  Args:
    source: Henrik
    type: :Man
  AssignClass (31622f93-2473-4493-b2ca-4b463b15d92c)
 Call ID: 31622f93-2473-4493-b2ca-4b463b15d92c
  Args:
    source: Henrik
    type: :Person
  AddTriple (62cd76ff-ee8b-4d5d-a0e3-5a55de5b3ad3)
 Call ID: 62cd76ff-ee8b-4d5d-a0e3-5a55de5b3ad3
  Args:
    relation: :isSiblingOf
    source: Athena_of_Monpezat
    target: Henrik
  AddTriple (97da0b4f-c7a1-487c-9182-ba289a10c250)
 Call ID: 97da0b4f-c7a1-487c-9182-ba289a10c250
  Args:
    relation: :isSiblingOf
    source: Athena_of_Monpezat
    target: Nikolai
  AddTriple (795283fc-58a6-4202-bac3-98a002d73d5e)
 Call ID: 795283fc-58a6-4202-bac3-98a002d73d5e
  Args:
    target: Felix
    source: Athena_of_Monpezat
    relation: :isSiblingOf
  Finish (63f7df76-5a4f-491f-98e8-261c35ca8c74)
 Call ID: 63f7df76-5a4f-491f-98e8-261c35ca8c74
  Args: