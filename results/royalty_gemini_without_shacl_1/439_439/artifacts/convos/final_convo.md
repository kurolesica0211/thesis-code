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
Lady Mary Cecilia Colman (née Bowes-Lyon; 30 January 1932 – 2 January 2021) was an English socialite, philanthropist, and extra lady-in-waiting to Princess Alexandra, The Honourable Lady Ogilvy.
The daughter of Michael Bowes-Lyon and Elizabeth Margaret Cator, her paternal aunt was Queen Elizabeth
The Queen Mother, and she was thus a first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
Early life

Mary Cecilia Bowes-Lyon was born on 30 January 1932 at Gastlings, the Bowes-Lyon family home in Biggleswade, Bedfordshire.
Her father, Michael Bowes-Lyon (1893–1953), was the fifth son of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne and Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne (née Cavendish-Bentinck).
Her mother, Elizabeth Margaret Cator (1899–1959), was a great-granddaughter of Charles Yorke, 4th Earl of Hardwicke.
She had a twin sister, Patricia Maud, later Lady Patricia Tetley, an older brother, Fergus Michael Claude, later Fergus Bowes-Lyon, 17th Earl of Strathmore and Kinghorne, and a younger brother, Michael Albemarle.
Lady Mary was also a godmother to Diana, Princess of Wales.
In 1949, a coming-out ball was held for her and her twin sister Patricia at Londonderry House, which was attended by their aunt, the Queen, and their cousins, The Princess Elizabeth and The Princess Margaret.
Marriage and children

On 10 November 1951 at St Bartholomew-the-Great in London, Mary married the then-Lieutenant Timothy Colman, son of the cricketer Geoffrey Colman.
Work and later life

In 1970, Mary was appointed an Extra Lady-in-waiting to another of the Queen's first cousins, Princess Alexandra, The Hon.
After her elder brother succeeded their cousin as 17th Earl of Strathmore and Kinghorne, she received the title and precedence of a daughter of an earl by royal warrant of precedence in 1974.
Lady Mary died at her home in Bixley, Norfolk on 2 January 2021, at the age of 88.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (406e5f93-fc93-4898-b0ea-67d538de2c0d)
 Call ID: 406e5f93-fc93-4898-b0ea-67d538de2c0d
  Args:
    type: :Woman
    source: Lady_Mary_Cecilia_Colman
  AssignClass (1b4f64f3-5e36-47d9-9281-7f1febe2674f)
 Call ID: 1b4f64f3-5e36-47d9-9281-7f1febe2674f
  Args:
    source: Lady_Mary_Cecilia_Colman
    type: :Person
  AddLiteral (4ebb5c2e-b9ab-4ca2-9ead-8d87fec34737)
 Call ID: 4ebb5c2e-b9ab-4ca2-9ead-8d87fec34737
  Args:
    relation: :hasBirthYear
    source: Lady_Mary_Cecilia_Colman
    literal_type: xsd:integer
    literal_value: 1932
  AddLiteral (9381d03d-984b-47c2-bd1a-05ce97f24c3a)
 Call ID: 9381d03d-984b-47c2-bd1a-05ce97f24c3a
  Args:
    relation: :hasDeathYear
    source: Lady_Mary_Cecilia_Colman
    literal_type: xsd:integer
    literal_value: 2021
  AssignClass (aecdfb2d-854e-4718-a64c-0e8f7b6d1b69)
 Call ID: aecdfb2d-854e-4718-a64c-0e8f7b6d1b69
  Args:
    type: :Man
    source: Michael_Bowes-Lyon
  AssignClass (f55f1d2f-51f5-447c-9219-6709a4dca3bf)
 Call ID: f55f1d2f-51f5-447c-9219-6709a4dca3bf
  Args:
    source: Michael_Bowes-Lyon
    type: :Person
  AssignClass (349e14f8-154c-4edd-8e4f-4f50c6247e40)
 Call ID: 349e14f8-154c-4edd-8e4f-4f50c6247e40
  Args:
    type: :Woman
    source: Elizabeth_Margaret_Cator
  AssignClass (3f0dc42c-355c-4174-9692-83d6a38ec77e)
 Call ID: 3f0dc42c-355c-4174-9692-83d6a38ec77e
  Args:
    source: Elizabeth_Margaret_Cator
    type: :Person
  AddTriple (b86c1e58-dc9a-491b-9cb5-5e07210d39ac)
 Call ID: b86c1e58-dc9a-491b-9cb5-5e07210d39ac
  Args:
    relation: :hasFather
    source: Lady_Mary_Cecilia_Colman
    target: Michael_Bowes-Lyon
  AddTriple (518bc849-a1b8-46be-8a8f-3a28be8a92e1)
 Call ID: 518bc849-a1b8-46be-8a8f-3a28be8a92e1
  Args:
    relation: :hasMother
    target: Elizabeth_Margaret_Cator
    source: Lady_Mary_Cecilia_Colman
  AssignClass (798eea18-90b7-4bd2-9288-2ef9e0940395)
 Call ID: 798eea18-90b7-4bd2-9288-2ef9e0940395
  Args:
    type: :Woman
    source: Patricia_Maud
  AssignClass (5ede53ba-9902-471b-a769-3af59e55e984)
 Call ID: 5ede53ba-9902-471b-a769-3af59e55e984
  Args:
    source: Patricia_Maud
    type: :Person
  AddTriple (ce2f9b0d-23ba-4a83-8d88-fdf79ba54fef)
 Call ID: ce2f9b0d-23ba-4a83-8d88-fdf79ba54fef
  Args:
    relation: :isSisterOf
    source: Lady_Mary_Cecilia_Colman
    target: Patricia_Maud
  AssignClass (18cce1e2-d441-4978-afc0-3bb592430bd3)
 Call ID: 18cce1e2-d441-4978-afc0-3bb592430bd3
  Args:
    source: Fergus_Michael_Claude
    type: :Man
  AssignClass (313c2980-e226-4a1a-a58f-8dbda813c767)
 Call ID: 313c2980-e226-4a1a-a58f-8dbda813c767
  Args:
    type: :Person
    source: Fergus_Michael_Claude
  AddTriple (d29054e0-c405-4369-9b79-38fe4900584f)
 Call ID: d29054e0-c405-4369-9b79-38fe4900584f
  Args:
    target: Fergus_Michael_Claude
    source: Lady_Mary_Cecilia_Colman
    relation: :hasBrother
  AssignClass (ac32903b-6e1d-4994-a3d1-e6c72a3e1ed0)
 Call ID: ac32903b-6e1d-4994-a3d1-e6c72a3e1ed0
  Args:
    source: Michael_Albemarle
    type: :Man
  AssignClass (2f1f6de4-7ba4-4d7b-a7e8-a84060b93011)
 Call ID: 2f1f6de4-7ba4-4d7b-a7e8-a84060b93011
  Args:
    type: :Person
    source: Michael_Albemarle
  AddTriple (94939118-9e23-468b-8899-05ec53518697)
 Call ID: 94939118-9e23-468b-8899-05ec53518697
  Args:
    relation: :hasBrother
    target: Michael_Albemarle
    source: Lady_Mary_Cecilia_Colman
  AssignClass (8ee6e7e3-4c8b-4351-adfc-738bb6a31f2b)
 Call ID: 8ee6e7e3-4c8b-4351-adfc-738bb6a31f2b
  Args:
    source: Timothy_Colman
    type: :Man
  AssignClass (01ae17fd-d440-47e3-a923-607d00415b88)
 Call ID: 01ae17fd-d440-47e3-a923-607d00415b88
  Args:
    type: :Person
    source: Timothy_Colman
  AddTriple (7b09ae14-a878-418d-92c3-5d2ea6ff01e0)
 Call ID: 7b09ae14-a878-418d-92c3-5d2ea6ff01e0
  Args:
    relation: :hasRelation
    target: Timothy_Colman
    source: Lady_Mary_Cecilia_Colman
  AddLiteral (aa352d9e-7a73-4343-8c8a-5d15ca8d4962)
 Call ID: aa352d9e-7a73-4343-8c8a-5d15ca8d4962
  Args:
    literal_value: 1951
    source: Lady_Mary_Cecilia_Colman
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (f3663984-a550-4118-bd35-9038208b71ee)
 Call ID: f3663984-a550-4118-bd35-9038208b71ee
  Args:
    type: :Man
    source: Geoffrey_Colman
  AssignClass (2c98b648-5c08-46c3-9928-8e9da03e8c73)
 Call ID: 2c98b648-5c08-46c3-9928-8e9da03e8c73
  Args:
    source: Geoffrey_Colman
    type: :Person
  AddTriple (c6ad5c01-a1c8-4079-b732-3be0f9bdcc0e)
 Call ID: c6ad5c01-a1c8-4079-b732-3be0f9bdcc0e
  Args:
    target: Geoffrey_Colman
    source: Timothy_Colman
    relation: :hasFather
  Finish (643bf78e-fb8b-467f-b50c-f212c015ed5f)
 Call ID: 643bf78e-fb8b-467f-b50c-f212c015ed5f
  Args: