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
  AssignClass (a0e2bebf-fd79-402b-8f55-70927e5680bb)
 Call ID: a0e2bebf-fd79-402b-8f55-70927e5680bb
  Args:
    type: :Woman
    source: Athena_of_Monpezat
  AssignClass (dd57eb1c-68fe-4280-84b1-8be578d83fbc)
 Call ID: dd57eb1c-68fe-4280-84b1-8be578d83fbc
  Args:
    type: :Person
    source: Athena_of_Monpezat
  AddLiteral (4247883d-d11a-46e5-8777-6c1b8414dab3)
 Call ID: 4247883d-d11a-46e5-8777-6c1b8414dab3
  Args:
    literal_value: Athena Marguerite Françoise Marie
    source: Athena_of_Monpezat
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (96cc3efd-2877-4e64-ad24-284b797db0e0)
 Call ID: 96cc3efd-2877-4e64-ad24-284b797db0e0
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Athena_of_Monpezat
    literal_value: 2012
  AssignClass (f43bec31-ee3c-478a-853c-609fd14b14cd)
 Call ID: f43bec31-ee3c-478a-853c-609fd14b14cd
  Args:
    type: :Man
    source: Joachim_of_Denmark
  AssignClass (6e965f11-4e75-425d-a12e-e7ba81406dec)
 Call ID: 6e965f11-4e75-425d-a12e-e7ba81406dec
  Args:
    type: :Person
    source: Joachim_of_Denmark
  AssignClass (cf8844e8-eae3-4501-afdc-60314be8ad81)
 Call ID: cf8844e8-eae3-4501-afdc-60314be8ad81
  Args:
    type: :Woman
    source: Marie_of_Denmark
  AssignClass (589bbdd7-2b02-43eb-acaa-66a47ef7e546)
 Call ID: 589bbdd7-2b02-43eb-acaa-66a47ef7e546
  Args:
    type: :Person
    source: Marie_of_Denmark
  AddTriple (6360ae65-ba44-46f8-8b5c-55195768798b)
 Call ID: 6360ae65-ba44-46f8-8b5c-55195768798b
  Args:
    relation: :hasFather
    source: Athena_of_Monpezat
    target: Joachim_of_Denmark
  AddTriple (7fc79c0f-285d-4749-95ee-6805fd30adca)
 Call ID: 7fc79c0f-285d-4749-95ee-6805fd30adca
  Args:
    target: Marie_of_Denmark
    source: Athena_of_Monpezat
    relation: :hasMother
  AssignClass (52b34229-8674-474a-88f8-a1a6f1a52df5)
 Call ID: 52b34229-8674-474a-88f8-a1a6f1a52df5
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (80567224-5469-4c76-9fb2-8ba6a7d3973d)
 Call ID: 80567224-5469-4c76-9fb2-8ba6a7d3973d
  Args:
    type: :Person
    source: Margrethe_II
  AssignClass (846172f5-96d1-474c-8e55-529ee643867f)
 Call ID: 846172f5-96d1-474c-8e55-529ee643867f
  Args:
    type: :Man
    source: Henrik_Prince_Consort
  AssignClass (1dddc9b6-f969-4cdf-962c-66ba4240a93a)
 Call ID: 1dddc9b6-f969-4cdf-962c-66ba4240a93a
  Args:
    type: :Person
    source: Henrik_Prince_Consort
  AddTriple (b9960fb4-c749-4972-b12a-19daea74b4ff)
 Call ID: b9960fb4-c749-4972-b12a-19daea74b4ff
  Args:
    source: Athena_of_Monpezat
    target: Margrethe_II
    relation: :hasAncestor
  AddTriple (a07bf08c-3b21-43c4-9177-0084b0f186a9)
 Call ID: a07bf08c-3b21-43c4-9177-0084b0f186a9
  Args:
    source: Athena_of_Monpezat
    target: Henrik_Prince_Consort
    relation: :hasAncestor
  AssignClass (7209fdad-610b-4882-a393-5af51b1f862b)
 Call ID: 7209fdad-610b-4882-a393-5af51b1f862b
  Args:
    type: :Man
    source: Frederik_X
  AssignClass (fc4d7622-7092-45f8-b3f6-e31561e12d3b)
 Call ID: fc4d7622-7092-45f8-b3f6-e31561e12d3b
  Args:
    type: :Person
    source: Frederik_X
  AssignClass (a6124a8b-4c69-406e-b281-e40c6f4878eb)
 Call ID: a6124a8b-4c69-406e-b281-e40c6f4878eb
  Args:
    type: :Man
    source: Nikolai_of_Monpezat
  AssignClass (cea5a22e-d241-42b1-a79e-e384e1bca818)
 Call ID: cea5a22e-d241-42b1-a79e-e384e1bca818
  Args:
    type: :Person
    source: Nikolai_of_Monpezat
  AssignClass (ed6b0d75-ab0b-4752-8036-a9208d99f95f)
 Call ID: ed6b0d75-ab0b-4752-8036-a9208d99f95f
  Args:
    type: :Man
    source: Felix_of_Monpezat
  AssignClass (4237d615-dbfe-4995-af0e-f1607bbc24a5)
 Call ID: 4237d615-dbfe-4995-af0e-f1607bbc24a5
  Args:
    type: :Person
    source: Felix_of_Monpezat
  AssignClass (a8bbe2ed-338d-40f0-9394-420c37d7c91a)
 Call ID: a8bbe2ed-338d-40f0-9394-420c37d7c91a
  Args:
    type: :Man
    source: Henrik_of_Monpezat
  AssignClass (202548bf-8d19-40ff-a1f7-fee223614cc6)
 Call ID: 202548bf-8d19-40ff-a1f7-fee223614cc6
  Args:
    type: :Person
    source: Henrik_of_Monpezat
  AddTriple (5b51d34c-06d3-4c01-a108-ab4d6551b38f)
 Call ID: 5b51d34c-06d3-4c01-a108-ab4d6551b38f
  Args:
    target: Henrik_of_Monpezat
    source: Athena_of_Monpezat
    relation: :isSiblingOf
  AddTriple (231cc18c-643b-48e0-946c-691ea928b7c6)
 Call ID: 231cc18c-643b-48e0-946c-691ea928b7c6
  Args:
    source: Athena_of_Monpezat
    target: Nikolai_of_Monpezat
    relation: :isSiblingOf
  AddTriple (0e02b45f-c7af-4e13-b088-bc55366833b3)
 Call ID: 0e02b45f-c7af-4e13-b088-bc55366833b3
  Args:
    relation: :isSiblingOf
    source: Athena_of_Monpezat
    target: Felix_of_Monpezat
  Finish (8e6e1bd8-4ff6-40e9-8a90-fb58bff53dbc)
 Call ID: 8e6e1bd8-4ff6-40e9-8a90-fb58bff53dbc
  Args: