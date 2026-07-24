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
Princess Irene of Greece and Denmark, Duchess of Aosta (Greek: Πριγκίπισσα Ειρήνη της Ελλάδας και Δανίας; 13 February 1904 – 15 April 1974) was the fifth child and second daughter of King Constantine I of Greece and the former Princess Sophie of Prussia (sister of Kaiser Wilhelm II of Germany).
She was a member of the Royal Families of Greece and Italy.
Family and early life

Her Royal Highness Princess Irene of Greece and Denmark was born on 13 February 1904 in Athens.
She had three elder brothers, George (1890), Alexander (1893) and Paul (1901), and one elder sister, Helen (1896).
In 1927, her brother, George, announced her engagement to Prince Christian of Schaumburg-Lippe, a nephew of Christian X of Denmark, but no marriage occurred.
Princess Irene’s paternal grandparents were King George I of Greece and his Queen, Grand Duchess Olga Konstantinovna of Russia.
Her maternal grandparents were German Emperor Frederick III, and his Empress Consort, Victoria, Princess Royal.
Empress Victoria was a daughter of Prince Albert of Saxe-Coburg and Gotha and Queen Victoria of the United Kingdom.
Marriage

Shortly afterwards, the Greek princess had to officially renounce the Orthodox faith and convert to the Catholic religion, as required by the laws of the House of Savoy.
On 1 July 1939, Princess Irene married Prince Aimone, 4th Duke of Aosta (9 March 1900 – 29 January 1948).
She was also a bridesmaid at the wedding of her cousin, Princess Marina of Greece and Denmark
In March 1942, Irene, who was a trained nurse, headed a Red Cross hospital train going to Russia to repatriate wounded Italian soldiers.
Prince Aimone became the 4th Duke of Aosta on 3 March 1942, following the death of his elder brother, Amedeo.
After the Allied armistice with the Kingdom of Italy, Irene was interned by the Germans at the Hotel Ifen in Hirschegg, Austria, July 1944, along with her infant son, her sister-in-law and two nieces.
Prince Aimone died on 29 January 1948 in Buenos Aires.
Upon his death, his son Amedeo succeeded him as the 5th Duke of Aosta.
In June 1948, the family was allowed to return to Italy, and Irene spent the rest of her life living outside of Florence where she became a member of the Dominican Third Order and continued her social work.
Irene died on 15 April 1974 in Fiesole, Italy, after fighting a long illness.
Finally, in 1996, the ashes of the Duke and Duchess of Aosta were transferred to one of the necropolises of the House of Savoy, at the Basilica of Superga in Turin.
Ancestry

References

Edward Hanson, The Wandering Princess: Princess Helene of France, Duchess of Aosta (1871-1951) .



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
  AssignClass (ba06cb77-3f01-4c74-b608-6450f3a2754d)
 Call ID: ba06cb77-3f01-4c74-b608-6450f3a2754d
  Args:
    type: :Woman
    source: :Irene_of_Greece_and_Denmark
  AssignClass (9d02a706-212b-4240-a016-9dbd6e8fb094)
 Call ID: 9d02a706-212b-4240-a016-9dbd6e8fb094
  Args:
    type: :Person
    source: :Irene_of_Greece_and_Denmark
  AddLiteral (c27bd861-31c0-40a4-b35d-28689add76f0)
 Call ID: c27bd861-31c0-40a4-b35d-28689add76f0
  Args:
    source: :Irene_of_Greece_and_Denmark
    literal_value: 1904
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (8ffcdcaf-8fae-4477-b870-fb7f49cdc696)
 Call ID: 8ffcdcaf-8fae-4477-b870-fb7f49cdc696
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1974
    source: :Irene_of_Greece_and_Denmark
  AssignClass (0acdf95a-43d0-4a4e-bc7a-58cd896accb0)
 Call ID: 0acdf95a-43d0-4a4e-bc7a-58cd896accb0
  Args:
    type: :Man
    source: :Constantine_I_of_Greece
  AssignClass (cbcf6da6-1c34-4ae3-8c5e-c12c96cacda2)
 Call ID: cbcf6da6-1c34-4ae3-8c5e-c12c96cacda2
  Args:
    type: :Person
    source: :Constantine_I_of_Greece
  AssignClass (ee33a5ec-e307-4a87-aedc-cdcbb33bb521)
 Call ID: ee33a5ec-e307-4a87-aedc-cdcbb33bb521
  Args:
    type: :Woman
    source: :Sophie_of_Prussia
  AssignClass (15867150-4a79-42cf-b238-c139ab585e73)
 Call ID: 15867150-4a79-42cf-b238-c139ab585e73
  Args:
    type: :Person
    source: :Sophie_of_Prussia
  AddTriple (faa47fa3-c617-4068-ac51-f93470bfbbbd)
 Call ID: faa47fa3-c617-4068-ac51-f93470bfbbbd
  Args:
    relation: :hasFather
    target: :Constantine_I_of_Greece
    source: :Irene_of_Greece_and_Denmark
  AddTriple (f8570114-d749-4909-b6fe-492b94ed54f9)
 Call ID: f8570114-d749-4909-b6fe-492b94ed54f9
  Args:
    relation: :hasMother
    target: :Sophie_of_Prussia
    source: :Irene_of_Greece_and_Denmark
  AssignClass (8b7a278a-5838-47d4-a898-4ca48093a596)
 Call ID: 8b7a278a-5838-47d4-a898-4ca48093a596
  Args:
    type: :Man
    source: :George_of_Greece
  AssignClass (59d61306-d528-42ef-af1b-fb0aa7607682)
 Call ID: 59d61306-d528-42ef-af1b-fb0aa7607682
  Args:
    type: :Person
    source: :George_of_Greece
  AssignClass (fab6e416-0813-4415-b1b5-49d0feae960e)
 Call ID: fab6e416-0813-4415-b1b5-49d0feae960e
  Args:
    type: :Man
    source: :Alexander_of_Greece
  AssignClass (ec6742db-9b3f-4ab6-812f-e16553d490e1)
 Call ID: ec6742db-9b3f-4ab6-812f-e16553d490e1
  Args:
    type: :Person
    source: :Alexander_of_Greece
  AssignClass (5b84990a-4234-44d8-9b83-b5ae0b605ac6)
 Call ID: 5b84990a-4234-44d8-9b83-b5ae0b605ac6
  Args:
    type: :Man
    source: :Paul_of_Greece
  AssignClass (28648726-6343-443d-b023-e00cc07a7dfb)
 Call ID: 28648726-6343-443d-b023-e00cc07a7dfb
  Args:
    type: :Person
    source: :Paul_of_Greece
  AssignClass (e618c538-3725-4215-a1db-4a3e8e926230)
 Call ID: e618c538-3725-4215-a1db-4a3e8e926230
  Args:
    type: :Woman
    source: :Helen_of_Greece
  AssignClass (fdc7a516-afe4-4650-a06a-14676ca7a3ac)
 Call ID: fdc7a516-afe4-4650-a06a-14676ca7a3ac
  Args:
    type: :Person
    source: :Helen_of_Greece
  AddTriple (1aa06085-7bb4-41bb-bcb1-310fa837e2df)
 Call ID: 1aa06085-7bb4-41bb-bcb1-310fa837e2df
  Args:
    relation: :hasBrother
    source: :Irene_of_Greece_and_Denmark
    target: :George_of_Greece
  AddTriple (c20ed3b1-8279-4b4d-8710-7ab7db2cb922)
 Call ID: c20ed3b1-8279-4b4d-8710-7ab7db2cb922
  Args:
    relation: :hasBrother
    source: :Irene_of_Greece_and_Denmark
    target: :Alexander_of_Greece
  AddTriple (51b056a2-0049-48da-940e-f80d01fa1bde)
 Call ID: 51b056a2-0049-48da-940e-f80d01fa1bde
  Args:
    source: :Irene_of_Greece_and_Denmark
    target: :Paul_of_Greece
    relation: :hasBrother
  AddTriple (d9136fda-2461-4096-89c9-c94d6f55b5f9)
 Call ID: d9136fda-2461-4096-89c9-c94d6f55b5f9
  Args:
    relation: :hasSister
    source: :Irene_of_Greece_and_Denmark
    target: :Helen_of_Greece
  AssignClass (5e9ae04e-fae0-4285-90a2-d9652c813c41)
 Call ID: 5e9ae04e-fae0-4285-90a2-d9652c813c41
  Args:
    type: :Man
    source: :Aimone_4th_Duke_of_Aosta
  AssignClass (0f8747f2-2203-45dd-bd3e-11b2bacdb1b3)
 Call ID: 0f8747f2-2203-45dd-bd3e-11b2bacdb1b3
  Args:
    type: :Person
    source: :Aimone_4th_Duke_of_Aosta
  AddLiteral (dddc1b8c-a04f-49ce-98f4-1e0e3b2f1494)
 Call ID: dddc1b8c-a04f-49ce-98f4-1e0e3b2f1494
  Args:
    literal_value: 1939
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Irene_of_Greece_and_Denmark
  AddTriple (eca02ad3-fa7f-46c0-983a-557b58a8f47f)
 Call ID: eca02ad3-fa7f-46c0-983a-557b58a8f47f
  Args:
    relation: :hasRelation
    source: :Irene_of_Greece_and_Denmark
    target: :Aimone_4th_Duke_of_Aosta
  AssignClass (8467951e-e4fe-43dc-8232-8453c4534e2a)
 Call ID: 8467951e-e4fe-43dc-8232-8453c4534e2a
  Args:
    type: :Man
    source: :Amedeo_5th_Duke_of_Aosta
  AssignClass (dc44d669-ddf3-4445-8768-7927750e44d5)
 Call ID: dc44d669-ddf3-4445-8768-7927750e44d5
  Args:
    type: :Person
    source: :Amedeo_5th_Duke_of_Aosta
  AddTriple (f799b45e-d94e-4d03-b330-c44ada0c5333)
 Call ID: f799b45e-d94e-4d03-b330-c44ada0c5333
  Args:
    relation: :hasSon
    target: :Amedeo_5th_Duke_of_Aosta
    source: :Irene_of_Greece_and_Denmark
  Finish (1f2ba697-59c2-4ab1-8ebc-3388e022d16c)
 Call ID: 1f2ba697-59c2-4ab1-8ebc-3388e022d16c
  Args: