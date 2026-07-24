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
Princess Maria di Grazia of Bourbon-Two Sicilies (12 August 1878 – 20 June 1973) was a Princess of Bourbon-Two Sicilies by birth as well as Princess Imperial of Brazil and Princess of Orleans-Braganza through her marriage to Prince Luiz of Orléans-Braganza, secondborn son and pretense heir of Isabel, Princess Imperial of Brazil.
Early life and family

Princess Maria was born at their parents' Villa Maria Teresa in Cannes, where her family had been exiled since the 1861 due to the Italian Unification.
She was the sixth child and third daughter of Prince Alfonso, Count of Caserta and his wife Princess Antonietta of Bourbon-Two Sicilies.
She was usually called “Maria Pia”.
Her father, the third son of King Ferdinand II of the Two Sicilies, became Head of the Royal House of the Two Sicilies with the death of his elder brother, King Francis II, in 1894.
Maria di Grazia was baptized and had Robert I, Duke of Parma, and his first wife, Princess Maria Pia of the Two Sicilies, as godparents.
Maria di Grazia and her sisters were educated at the College of the Sacred Heart of Aix-Provence, an institution run by nuns near Cannes.
There, Maria di Grazia spent her childhood and, after finishing her studies, her youth.
In one of the visits of the Emperor Pedro II of Brazil to Cannes, he visited the Villa Maria Teresa.
The Count of Caserta gathered all his children to present them to the monarch, and Maria di Grazia, at the age of ten, had to play "Turkish March" by Mozart, on the piano.
Upon turning 18, Maria di Grazia was taken with her sisters to be presented to the court of Emperor Franz Joseph I of Austria.
After Austria, the princesses were taken to Munich, where they were given a gala lunch by Luitpold, Prince Regent of Bavaria.
Marriage and issue

Princess Maria di Grazia met her future fiancé when they were still young, when Luiz eventually arrived in Europe due to the exile imposed by the proclamation of the republic in Brazil in 1889.
They later reconnected in 1903 when Prince Luiz, then serving in the Austrian Army, was visiting several relatives in France.
On 4 November 1908 Princess Maria di Grazia married Prince Luiz Maria of Orléans-Braganza, son of Prince Gaston of Orléans, Count of Eu and Isabel, Princess Imperial of Brazil, in Cannes.
Later life

Prince Luiz died in 1920 leaving Maria a widow for the remainder of her life.
In 1922, Maria accompanied the Brazilian Imperial Family to Brazil for the country's centennial celebrations of its independence.
During the course of the trip, the Count of Eu died while recumbent upon her shoulder.
After that, Princess Maria preferred to live with her children in France, where they could have a better education.
}} Media related to Princess Maria di Grazia of the Two Sicilies at Wikimedia Commons



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
  AssignClass (65d680f0-3301-4e9f-be38-9d92fab9b6c8)
 Call ID: 65d680f0-3301-4e9f-be38-9d92fab9b6c8
  Args:
    type: :Woman
    source: Maria_di_Grazia
  AssignClass (5f4eae0b-b8b0-4d9c-83a7-7c80551ccb4e)
 Call ID: 5f4eae0b-b8b0-4d9c-83a7-7c80551ccb4e
  Args:
    source: Maria_di_Grazia
    type: :Person
  AddLiteral (5138e5bd-7d52-4cb6-ac24-135ad3f2486e)
 Call ID: 5138e5bd-7d52-4cb6-ac24-135ad3f2486e
  Args:
    literal_type: xsd:integer
    source: Maria_di_Grazia
    literal_value: 1878
    relation: :hasBirthYear
  AddLiteral (c30b650e-c352-425f-93ea-b7601df99d75)
 Call ID: c30b650e-c352-425f-93ea-b7601df99d75
  Args:
    literal_type: xsd:integer
    literal_value: 1973
    source: Maria_di_Grazia
    relation: :hasDeathYear
  AddLiteral (949036eb-4e76-454f-94a4-ef268cc5b656)
 Call ID: 949036eb-4e76-454f-94a4-ef268cc5b656
  Args:
    literal_value: Maria Pia
    source: Maria_di_Grazia
    literal_type: xsd:string
    relation: :knownAs
  AssignClass (5808b2de-b98b-4115-8122-1092f7fbc82f)
 Call ID: 5808b2de-b98b-4115-8122-1092f7fbc82f
  Args:
    type: :Man
    source: Prince_Alfonso
  AssignClass (cc6902a5-06bc-471f-a43a-8cb584a09eb2)
 Call ID: cc6902a5-06bc-471f-a43a-8cb584a09eb2
  Args:
    source: Prince_Alfonso
    type: :Person
  AssignClass (c713ffa2-4a8c-4167-85c9-cf64095534e0)
 Call ID: c713ffa2-4a8c-4167-85c9-cf64095534e0
  Args:
    source: Prince_Alfonso
    type: :Ancestor
  AssignClass (28ca83f5-1a60-47a7-853e-a72de71f4290)
 Call ID: 28ca83f5-1a60-47a7-853e-a72de71f4290
  Args:
    type: :Woman
    source: Princess_Antonietta
  AssignClass (53d84f42-7256-4157-a039-c80e4e08f0dd)
 Call ID: 53d84f42-7256-4157-a039-c80e4e08f0dd
  Args:
    type: :Person
    source: Princess_Antonietta
  AssignClass (389dfbdd-0ade-4616-a042-27028018d297)
 Call ID: 389dfbdd-0ade-4616-a042-27028018d297
  Args:
    source: Princess_Antonietta
    type: :Ancestor
  AddTriple (019fd1a1-0d63-4348-998e-1c2c6d145491)
 Call ID: 019fd1a1-0d63-4348-998e-1c2c6d145491
  Args:
    target: Prince_Alfonso
    source: Maria_di_Grazia
    relation: :hasFather
  AddTriple (d15869db-2432-4428-8311-9080c5aacd12)
 Call ID: d15869db-2432-4428-8311-9080c5aacd12
  Args:
    relation: :hasMother
    source: Maria_di_Grazia
    target: Princess_Antonietta
  AssignClass (06c53bf6-2a15-414e-aa8d-d3a3f7f9ee61)
 Call ID: 06c53bf6-2a15-414e-aa8d-d3a3f7f9ee61
  Args:
    type: :Man
    source: King_Ferdinand_II
  AssignClass (dccd2371-f17d-4451-baec-8d8c50bc852e)
 Call ID: dccd2371-f17d-4451-baec-8d8c50bc852e
  Args:
    source: King_Ferdinand_II
    type: :Person
  AssignClass (f4170970-5701-4e1b-ab3d-c3cd0899ed55)
 Call ID: f4170970-5701-4e1b-ab3d-c3cd0899ed55
  Args:
    source: King_Ferdinand_II
    type: :Ancestor
  AddTriple (bd9f7a57-54aa-44f3-9028-d30afb2f98e0)
 Call ID: bd9f7a57-54aa-44f3-9028-d30afb2f98e0
  Args:
    relation: :hasFather
    source: Prince_Alfonso
    target: King_Ferdinand_II
  AssignClass (40a3fc6e-eded-450f-b1d8-088ca1ad4ef1)
 Call ID: 40a3fc6e-eded-450f-b1d8-088ca1ad4ef1
  Args:
    source: King_Francis_II
    type: :Man
  AssignClass (6d7ac680-2f7e-42d2-984e-1a921ed4b279)
 Call ID: 6d7ac680-2f7e-42d2-984e-1a921ed4b279
  Args:
    source: King_Francis_II
    type: :Person
  AddTriple (faaa5d23-82d1-4587-bc2b-6d6a6b04638f)
 Call ID: faaa5d23-82d1-4587-bc2b-6d6a6b04638f
  Args:
    source: King_Francis_II
    target: Prince_Alfonso
    relation: :isBrotherOf
  AssignClass (592db57d-9c38-4254-9b26-294dd2406827)
 Call ID: 592db57d-9c38-4254-9b26-294dd2406827
  Args:
    source: Prince_Luiz_Maria
    type: :Man
  AssignClass (da31bcc7-6038-4fc5-aeaa-ab4a2b7aa2e4)
 Call ID: da31bcc7-6038-4fc5-aeaa-ab4a2b7aa2e4
  Args:
    source: Prince_Luiz_Maria
    type: :Person
  AddLiteral (76e4bd03-2587-47c7-89b4-42cfef9bd088)
 Call ID: 76e4bd03-2587-47c7-89b4-42cfef9bd088
  Args:
    relation: :hasMarriageYear
    literal_value: 1908
    source: Maria_di_Grazia
    literal_type: xsd:integer
  AddTriple (2b3d9b68-f1c7-4e74-94d4-762626056a6d)
 Call ID: 2b3d9b68-f1c7-4e74-94d4-762626056a6d
  Args:
    relation: :hasRelation
    source: Maria_di_Grazia
    target: Prince_Luiz_Maria
  AssignClass (7c6c75cf-5d28-4323-95b8-cdaea3ba8879)
 Call ID: 7c6c75cf-5d28-4323-95b8-cdaea3ba8879
  Args:
    type: :Man
    source: Prince_Gaston_of_Orleans
  AssignClass (56a04026-9402-4b47-9b2c-151ffb943e57)
 Call ID: 56a04026-9402-4b47-9b2c-151ffb943e57
  Args:
    type: :Person
    source: Prince_Gaston_of_Orleans
  AssignClass (5d3141a1-9215-4ccb-ae5c-634dfd291fac)
 Call ID: 5d3141a1-9215-4ccb-ae5c-634dfd291fac
  Args:
    source: Prince_Gaston_of_Orleans
    type: :Ancestor
  AssignClass (bf8de55b-69dc-4dea-8224-45e30ec7a6b2)
 Call ID: bf8de55b-69dc-4dea-8224-45e30ec7a6b2
  Args:
    source: Isabel_Princess_Imperial_of_Brazil
    type: :Woman
  AssignClass (ff2da910-dd82-43ea-82e3-67134d5541d8)
 Call ID: ff2da910-dd82-43ea-82e3-67134d5541d8
  Args:
    type: :Person
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (bd5ff584-f67d-418a-97bc-7b5bfd85e8a0)
 Call ID: bd5ff584-f67d-418a-97bc-7b5bfd85e8a0
  Args:
    type: :Ancestor
    source: Isabel_Princess_Imperial_of_Brazil
  AddTriple (d8516fe0-6857-4476-9e2e-64ef5c5eee1e)
 Call ID: d8516fe0-6857-4476-9e2e-64ef5c5eee1e
  Args:
    source: Prince_Luiz_Maria
    target: Prince_Gaston_of_Orleans
    relation: :hasFather
  AddTriple (00711788-ae19-4898-8997-e3d9ea906798)
 Call ID: 00711788-ae19-4898-8997-e3d9ea906798
  Args:
    target: Isabel_Princess_Imperial_of_Brazil
    source: Prince_Luiz_Maria
    relation: :hasMother
  AddLiteral (f514d7ce-4c6c-41eb-99aa-331367a098a3)
 Call ID: f514d7ce-4c6c-41eb-99aa-331367a098a3
  Args:
    relation: :hasDeathYear
    literal_value: 1920
    source: Prince_Luiz_Maria
    literal_type: xsd:integer
  Finish (54162710-2c81-42de-af88-ddb628a77155)
 Call ID: 54162710-2c81-42de-af88-ddb628a77155
  Args: