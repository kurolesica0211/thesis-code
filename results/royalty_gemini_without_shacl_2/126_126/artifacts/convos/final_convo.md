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
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


The Duke of CalabriaThe Duchess of Calabria


Princess Anne of Bourbon-Two Sicilies, Dowager Duchess of Calabria (Anne Marguerite Brigitte Marie; born 4 December 1938), born Princess Anne  of Orléans, is the widow of Infante Carlos, Duke of Calabria.
She is the third daughter and fifth child of Henri, Count of Paris, Orléanist claimant to the defunct French throne, and his wife Princess Isabelle of Orléans-Braganza.
Biography

Princess Anne of Orléans was born on 4 December 1938 at Woluwe-Saint-Pierre, Belgium, to Henri, Count of Paris, claimant to the French throne, and Princess Isabelle of Orléans-Braganza.
At the time, the family was residing at Manoir d'Anjou, a 15-hectare estate in the Belgian town.
Since her marriage, Princess Anne has accompanied her husband, and now son, on official engagements on behalf of the Sacred Military Constantinian Order of Saint George.
Due to the close friendship and familial relationship between her husband and King Juan Carlos, Princess Anne and her husband were viewed as extended members of the Spanish royal family.
The Duchess of Calabria occasionally undertakes official engagements on behalf of the Spanish monarchy.
Marriage and issue

Princess Anne became romantically involved with Prince Carlos, Duke of Noto, son and heir of Infante Alfonso, Duke of Calabria, whom she had known since childhood, at the wedding of the future King Juan Carlos I of Spain and Princess Sophia of Greece and Denmark in Athens in 1962.
The Count of Paris initially withheld his consent to the match as he supported the claim of Prince Ranieri, Duke of Castro to the defunct throne of the Kingdom of the Two Sicilies.
Eventually, after years of waiting and the death of Prince Carlos's father, the Count of Paris relented and the engagement was announced.
The 250 guests received one of two different invitations from either the bride's parents or the groom's; the former referred to the bride's marriage to "HRH Prince Carlos of Bourbon," while the latter announced the wedding of "Princess Anne of France" to the "Duke of Calabria.
The following day, on 12 May, the religious marriage was held at the Chapelle royale de Dreux, the traditional marriage and burial place of the House of Orléans.
The Duke and Duchess of Calabria made their home in Spain.
They remained married for 50 years until the Duke's death on 5 October 2015.
Anne was titled HRH
The Dowager Duchess of Calabria only after the death of her mother-in-law, Infanta Alicia, Duchess of Calabria, in 2017; from 2015 to 2017 she was officially addressed as HRH Infanta Anne, Duchess of Calabria.
The Duke and Duchess of Calabria had five children:


Honours

Arms

Ancestors

References



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
  AssignClass (e22e2291-4a70-4731-81e6-ec70fd360072)
 Call ID: e22e2291-4a70-4731-81e6-ec70fd360072
  Args:
    type: :Person
    source: :Princess_Anne_of_Orleans
  AssignClass (361600bf-0823-4d38-b4ed-21d3a54da6fd)
 Call ID: 361600bf-0823-4d38-b4ed-21d3a54da6fd
  Args:
    type: :Woman
    source: :Princess_Anne_of_Orleans
  AddLiteral (868f7bf3-44c4-485f-9c63-eb2d49ec9096)
 Call ID: 868f7bf3-44c4-485f-9c63-eb2d49ec9096
  Args:
    source: :Princess_Anne_of_Orleans
    literal_type: xsd:integer
    literal_value: 1938
    relation: :hasBirthYear
  AssignClass (4f51932b-780c-49fc-bec6-804bcfe73fec)
 Call ID: 4f51932b-780c-49fc-bec6-804bcfe73fec
  Args:
    type: :Person
    source: :Henri_Count_of_Paris
  AssignClass (685e9be9-090c-42b3-a944-8f48dcd60af6)
 Call ID: 685e9be9-090c-42b3-a944-8f48dcd60af6
  Args:
    type: :Man
    source: :Henri_Count_of_Paris
  AssignClass (3172c9b7-8ed6-4284-9026-f00a084c75da)
 Call ID: 3172c9b7-8ed6-4284-9026-f00a084c75da
  Args:
    type: :Person
    source: :Princess_Isabelle_of_Orleans_Braganza
  AssignClass (4eb35673-c8a8-4dc9-9d97-73d3b5db3423)
 Call ID: 4eb35673-c8a8-4dc9-9d97-73d3b5db3423
  Args:
    type: :Woman
    source: :Princess_Isabelle_of_Orleans_Braganza
  AddTriple (eee0eb0a-9fa4-49df-943f-7452d3c21e19)
 Call ID: eee0eb0a-9fa4-49df-943f-7452d3c21e19
  Args:
    relation: :hasFather
    target: :Henri_Count_of_Paris
    source: :Princess_Anne_of_Orleans
  AddTriple (60a9ddf8-ba03-42e8-8e0c-976aa0a8d027)
 Call ID: 60a9ddf8-ba03-42e8-8e0c-976aa0a8d027
  Args:
    target: :Princess_Isabelle_of_Orleans_Braganza
    relation: :hasMother
    source: :Princess_Anne_of_Orleans
  AssignClass (fbc13274-ac85-4642-b80f-c5e93a5912b5)
 Call ID: fbc13274-ac85-4642-b80f-c5e93a5912b5
  Args:
    type: :Person
    source: :Infante_Carlos_Duke_of_Calabria
  AssignClass (b7fd5939-7d64-4814-a4bf-2fcca7ed36b4)
 Call ID: b7fd5939-7d64-4814-a4bf-2fcca7ed36b4
  Args:
    type: :Man
    source: :Infante_Carlos_Duke_of_Calabria
  AddTriple (4e640ca3-db5e-407f-a664-e0143e83b845)
 Call ID: 4e640ca3-db5e-407f-a664-e0143e83b845
  Args:
    target: :Infante_Carlos_Duke_of_Calabria
    relation: :hasRelation
    source: :Princess_Anne_of_Orleans
  AddLiteral (eb16730e-d8b6-4ef9-a026-12f015ed0194)
 Call ID: eb16730e-d8b6-4ef9-a026-12f015ed0194
  Args:
    relation: :hasDeathYear
    literal_value: 2015
    source: :Infante_Carlos_Duke_of_Calabria
    literal_type: xsd:integer
  AssignClass (3f1dd052-fd64-4c55-81bb-b6373c8e312f)
 Call ID: 3f1dd052-fd64-4c55-81bb-b6373c8e312f
  Args:
    type: :Person
    source: :Infante_Alfonso_Duke_of_Calabria
  AssignClass (63011c49-bf88-4800-be54-0c771d659792)
 Call ID: 63011c49-bf88-4800-be54-0c771d659792
  Args:
    type: :Man
    source: :Infante_Alfonso_Duke_of_Calabria
  AddTriple (9aebf44c-8d40-45d1-be17-6883f6923703)
 Call ID: 9aebf44c-8d40-45d1-be17-6883f6923703
  Args:
    source: :Infante_Carlos_Duke_of_Calabria
    relation: :hasFather
    target: :Infante_Alfonso_Duke_of_Calabria
  AssignClass (b792d9bc-7775-49c7-b7b3-b1c55b877d00)
 Call ID: b792d9bc-7775-49c7-b7b3-b1c55b877d00
  Args:
    type: :Person
    source: :Infanta_Alicia_Duchess_of_Calabria
  AssignClass (2f016c74-fd7a-431d-acae-b635f87f82c1)
 Call ID: 2f016c74-fd7a-431d-acae-b635f87f82c1
  Args:
    type: :Woman
    source: :Infanta_Alicia_Duchess_of_Calabria
  AddLiteral (3db98dc6-cb80-4d24-935b-3840ad7988e4)
 Call ID: 3db98dc6-cb80-4d24-935b-3840ad7988e4
  Args:
    literal_type: xsd:integer
    source: :Infanta_Alicia_Duchess_of_Calabria
    relation: :hasDeathYear
    literal_value: 2017
  AssignClass (40ea950b-69fd-4754-a2f9-fb04be30bc4a)
 Call ID: 40ea950b-69fd-4754-a2f9-fb04be30bc4a
  Args:
    type: :Person
    source: :King_Juan_Carlos_I
  AssignClass (f26b3707-4521-4b04-a4fe-e6549cb07ecb)
 Call ID: f26b3707-4521-4b04-a4fe-e6549cb07ecb
  Args:
    type: :Man
    source: :King_Juan_Carlos_I
  AssignClass (051bf57f-dc9e-4f61-8e6b-0ffce1dc9af2)
 Call ID: 051bf57f-dc9e-4f61-8e6b-0ffce1dc9af2
  Args:
    type: :Person
    source: :Queen_Sofia
  AssignClass (a1b68534-625b-484d-9ea7-a521da283aa8)
 Call ID: a1b68534-625b-484d-9ea7-a521da283aa8
  Args:
    type: :Woman
    source: :Queen_Sofia
  AddTriple (aecfb80f-a48c-4be7-a1c6-0bfa9d1fbe07)
 Call ID: aecfb80f-a48c-4be7-a1c6-0bfa9d1fbe07
  Args:
    source: :King_Juan_Carlos_I
    target: :Queen_Sofia
    relation: :hasRelation
  Finish (7c3ffcf8-173d-4850-9285-5040cf97a621)
 Call ID: 7c3ffcf8-173d-4850-9285-5040cf97a621
  Args: