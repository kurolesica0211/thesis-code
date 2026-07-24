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
María de las Mercedes, Princess of Asturias (María de las Mercedes de Borbón y Habsburgo-Lorena; 11 September 1880 – 17 October 1904) was the eldest child of King Alfonso XII of Spain and his second wife, Maria Christina of Austria.
She was Princess of Asturias, the heiress presumptive to the Crown of Spain, for all 24 years of her life.
Had her younger sibling, unborn at the death of Alfonso XII, been a daughter, Mercedes would have been Queen of Spain.
The sibling proved to be a boy, Alfonso XIII, and upon his birth in 1886, he was King, and Mercedes turned out not to be queen.
She resumed the position of heiress presumptive, which she held until her own death (aged 24), and was succeeded in it by her own infant son Alfonso, Alfonso XIII having not yet married and fathered a legitimate child.
Mercedes married in Madrid on 14 February 1901, her second cousin, Prince Carlos of Bourbon-Two Sicilies, a nephew of the King of the then-defunct Kingdom of the Two Sicilies, who was elevated to the rank of Infante of Spain.
Early life

Born on 11 September 1880 at the Royal Palace of Madrid, Mercedes was the first child of King Alfonso XII and his second wife, Maria Christina of Austria.
She was christened María de las Mercedes Isabel Teresa Cristina Alfonsa.
To smooth things out, Queen Maria Christina suggested giving their new daughter the name Mercedes in honor of her husband's first wife and Queen, Mercedes of Orléans.
Mercedes was heiress presumptive at birth, but the disappointment was so great that she was initially treated only as an infanta.
Antonio Cánovas del Castillo, then head of the government, who disliked Maria Christina and did not want the crown to pass again to a female after the disastrous reign of Isabella II, decided functionally to ignore the newborn.
Mercedes's paternal aunt Isabella retained the title of Princess of Asturias until Práxedes Mateo Sagasta, President of the government that had replaced Cánovas, pressured King Alfonso XII to accord the title to Mercedes, which he did on 10 March 1881.
On 12 November 1882, Mercedes gained a sister, Infanta Maria Teresa.
Alfonso had married Maria Christina in order to secure the succession to the throne.
In July 1883, Maria Christina left the Spanish court and traveled with her daughters to visit her own family in Austria.
By the summer of 1884, Alfonso XII's health had deteriorated: he had tuberculosis.
Given the nascent pregnancy, Mercedes was not declared queen because she would be displaced if a son was born — instead, there was a six month interregnum until the birth of her brother Alfonso XIII on 17 May 1886, who assumed the throne as king immediately upon birth.
Had the pregnancy been lost or resulted in another daughter, Mercedes would have been declared queen regnant and been retroactively recognized as having assumed the throne at the death of her father (there would have been no interregnum).
Instead, with the late king's new issue arriving, and being a boy, Mercedes resumed the position of heiress presumptive, a title she would continue to hold for the rest of her short life.
Education

Mercedes made her first public appearance at the royal court by the hand of her mother when Queen Maria Christina was declared regent.
The education of the Princess of Asturias and her younger sister Infanta Maria Teresa was confined to the Royal Palace of Madrid in an austere environment headed by two widows: their mother and their paternal aunt Isabella (herself formerly Princess of Asturias).
Despite her constitutional status, Mercedes was not given an education that would have prepared her to govern the nation.
Mercedes grew up to be a serious young woman, shy and unprepossessing.
In her adolescence, Mercedes accompanied her mother on trips abroad visiting her paternal grandmother in Paris, her paternal aunt Paz in Munich, and her maternal grandmother Elisabeth Franziska in Vienna.
The situation in Spain became more complicated with the Spanish–American War in 1898.
Mercedes and her sister lived a restricted life.
At the dance, Mercedes fell in love with her cousin Prince Carlos of Bourbon-Two Sicilies, and the two were frequently seen together.
Marriage

Prince Carlos, Queen Maria Christina's first cousin once removed, belonged to the deposed royal family of the Two Sicilies and had arrived in Spain years earlier in order to follow a military career in the Spanish army.
The pairing of the princess and Prince Carlos was not accidental.
He had been chosen as a prospective husband by both Queen Maria Christina and Infanta Isabella, who was his aunt as well.
It was considered paramount to marry Mercedes to a member of the Bourbon family in order to avoid a change of the dynasty in case she succeeded her brother.
Prince Carlos offered other advantages as groom to the Princess of Asturias.
As he did not belong to a reigning royal family, he could settle permanently in Spain and adopt the necessary Spanish nationality.
Carlos was of serious character, shy, handsome, and Mercedes was attracted to him.
It was feared that Caserta's son marrying Mercedes would bring the Carlist party too close to the Spanish throne.
Even the Prince's name – Carlos – aroused suspicion.
There were bitter attacks against Mercedes's marriage in the newspapers and protest on the streets in Madrid, Seville and Granada.
The Archbishop of Valladolid, one of Spain’s most prominent prelates, wrote a letter to the Queen warning her against the dire consequences if the marriage would take place.
Mercedes herself expressed her frustration to the strong opposition to her choice of groom in a letter to her aunt Paz: "I am happy to marry him, but I am also upset at those who have created such a fuss and made mother suffer for this... all because his father fought alongside don Carlos.
Death

The couple lived at the Royal Palace of Madrid in close proximity to Queen Maria Christina, who wished for such proximity.
The union was happy and two children were born in quick succession: Prince Alfonso (1901–1964) and Prince Fernando (1903–1905).
Pregnant for the third time, Mercedes longed for a daughter after having two sons.
The following month, twenty days before her due day, Mercedes fell seriously ill.
Peritonitis set in and on the early hours on 16 October 1904 Mercedes gave birth prematurely to her third child, Princess Isabella Alfonsa (1904–1985).
The health of the mother was so seriously compromised that little attention was given to the child, who was believed to have been stillborn until the young King Alfonso realized the baby was alive.
Mercedes died the following day, on 17 October 1904, surrounded by her family.
Mercedes' three children were left in the care of Queen Maria Christina and raised in the court of King Alfonso XIII.
The elder son was not given the title of Prince of Asturias, but replaced his mother as heir presumptive.



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
  AssignClass (6ab3d1cf-9c04-46af-b906-a279072d5b0b)
 Call ID: 6ab3d1cf-9c04-46af-b906-a279072d5b0b
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes
  AssignClass (c1fb4a17-f042-46fa-89a2-ec4563b219bd)
 Call ID: c1fb4a17-f042-46fa-89a2-ec4563b219bd
  Args:
    source: Maria_de_las_Mercedes
    type: :Person
  AssignClass (b22b0dd5-4994-406e-8e40-934e18b0873c)
 Call ID: b22b0dd5-4994-406e-8e40-934e18b0873c
  Args:
    type: :Man
    source: Alfonso_XII
  AssignClass (49dbb10b-037b-4d22-aa83-157e4da686fb)
 Call ID: 49dbb10b-037b-4d22-aa83-157e4da686fb
  Args:
    source: Alfonso_XII
    type: :Person
  AssignClass (77d8e616-63de-409a-8c99-79b8f3aa40bc)
 Call ID: 77d8e616-63de-409a-8c99-79b8f3aa40bc
  Args:
    type: :Woman
    source: Maria_Christina_of_Austria
  AssignClass (7b5bddd9-1b32-42d0-917e-ca62908958b1)
 Call ID: 7b5bddd9-1b32-42d0-917e-ca62908958b1
  Args:
    source: Maria_Christina_of_Austria
    type: :Person
  AssignClass (c2080854-1874-42fd-8615-b37e07e255cd)
 Call ID: c2080854-1874-42fd-8615-b37e07e255cd
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (c00b862c-4317-42df-9c22-c6e0d635db1b)
 Call ID: c00b862c-4317-42df-9c22-c6e0d635db1b
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (af464c3b-7232-4fc7-8575-a70e058ab7b4)
 Call ID: af464c3b-7232-4fc7-8575-a70e058ab7b4
  Args:
    source: Maria_Teresa
    type: :Woman
  AssignClass (c010706d-c532-4391-a976-9539313d6bdb)
 Call ID: c010706d-c532-4391-a976-9539313d6bdb
  Args:
    source: Maria_Teresa
    type: :Person
  AssignClass (90929e6b-5349-4c68-af68-9ba935a3a1db)
 Call ID: 90929e6b-5349-4c68-af68-9ba935a3a1db
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (57d514d1-29f3-43fb-b098-bca2c749d205)
 Call ID: 57d514d1-29f3-43fb-b098-bca2c749d205
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (ef937d19-a295-4014-b90c-3c7a94f5b2d6)
 Call ID: ef937d19-a295-4014-b90c-3c7a94f5b2d6
  Args:
    type: :Man
    source: Alfonso_son_of_Mercedes
  AssignClass (2869a1db-b08e-4800-9ba8-3703b99e8c50)
 Call ID: 2869a1db-b08e-4800-9ba8-3703b99e8c50
  Args:
    type: :Person
    source: Alfonso_son_of_Mercedes
  AssignClass (4a8fcdbf-65b9-48c4-a75b-1c8e7179e110)
 Call ID: 4a8fcdbf-65b9-48c4-a75b-1c8e7179e110
  Args:
    source: Fernando_son_of_Mercedes
    type: :Man
  AssignClass (024b4bd2-5c40-4e3b-8cc2-df072cfadfea)
 Call ID: 024b4bd2-5c40-4e3b-8cc2-df072cfadfea
  Args:
    source: Fernando_son_of_Mercedes
    type: :Person
  AssignClass (d442a349-4ced-4826-9ddf-2b074e07317e)
 Call ID: d442a349-4ced-4826-9ddf-2b074e07317e
  Args:
    source: Isabella_Alfonsa
    type: :Woman
  AssignClass (0e28222a-8847-43d2-b98c-95e3949cfe09)
 Call ID: 0e28222a-8847-43d2-b98c-95e3949cfe09
  Args:
    source: Isabella_Alfonsa
    type: :Person
  AddTriple (4b357d25-1b51-4006-bf1e-3d97e0a23297)
 Call ID: 4b357d25-1b51-4006-bf1e-3d97e0a23297
  Args:
    target: Alfonso_XII
    source: Maria_de_las_Mercedes
    relation: :hasFather
  AddTriple (1578f8da-984d-419f-aee0-ef9433560dd6)
 Call ID: 1578f8da-984d-419f-aee0-ef9433560dd6
  Args:
    target: Maria_Christina_of_Austria
    source: Maria_de_las_Mercedes
    relation: :hasMother
  AddTriple (57492114-01fa-45aa-80ab-8340ed60b465)
 Call ID: 57492114-01fa-45aa-80ab-8340ed60b465
  Args:
    target: Alfonso_XII
    source: Alfonso_XIII
    relation: :hasFather
  AddTriple (01e8c275-370a-4366-9bbc-3029b7880f75)
 Call ID: 01e8c275-370a-4366-9bbc-3029b7880f75
  Args:
    source: Alfonso_XIII
    target: Maria_Christina_of_Austria
    relation: :hasMother
  AddTriple (8dc69d34-836e-4f04-80af-12bb3ac5dddd)
 Call ID: 8dc69d34-836e-4f04-80af-12bb3ac5dddd
  Args:
    relation: :hasFather
    target: Alfonso_XII
    source: Maria_Teresa
  AddTriple (4ff7c36a-b3d4-431d-ae65-52622cf22126)
 Call ID: 4ff7c36a-b3d4-431d-ae65-52622cf22126
  Args:
    target: Maria_Christina_of_Austria
    source: Maria_Teresa
    relation: :hasMother
  AddTriple (bd87e528-f3aa-4e47-b7f6-8c13c79508ab)
 Call ID: bd87e528-f3aa-4e47-b7f6-8c13c79508ab
  Args:
    relation: :hasFather
    target: Carlos_of_Bourbon-Two_Sicilies
    source: Alfonso_son_of_Mercedes
  AddTriple (16754586-1370-4609-b4a4-e66c10425b25)
 Call ID: 16754586-1370-4609-b4a4-e66c10425b25
  Args:
    relation: :hasMother
    source: Alfonso_son_of_Mercedes
    target: Maria_de_las_Mercedes
  AddTriple (35beab02-21cc-41b8-b6db-545b7a7704f6)
 Call ID: 35beab02-21cc-41b8-b6db-545b7a7704f6
  Args:
    relation: :hasFather
    target: Carlos_of_Bourbon-Two_Sicilies
    source: Fernando_son_of_Mercedes
  AddTriple (d099f262-9531-4907-b81c-fd1c8335f020)
 Call ID: d099f262-9531-4907-b81c-fd1c8335f020
  Args:
    relation: :hasMother
    source: Fernando_son_of_Mercedes
    target: Maria_de_las_Mercedes
  AddTriple (2082b74c-560b-499d-823c-1d1e12f116ca)
 Call ID: 2082b74c-560b-499d-823c-1d1e12f116ca
  Args:
    source: Isabella_Alfonsa
    target: Carlos_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (840c63a3-4c7f-47d5-93f8-a4a5b9848943)
 Call ID: 840c63a3-4c7f-47d5-93f8-a4a5b9848943
  Args:
    relation: :hasMother
    target: Maria_de_las_Mercedes
    source: Isabella_Alfonsa
  AddLiteral (882e27c2-bd53-4b9f-8711-131809542f65)
 Call ID: 882e27c2-bd53-4b9f-8711-131809542f65
  Args:
    literal_type: xsd:string
    literal_value: 1880
    source: Maria_de_las_Mercedes
    relation: :hasBirthYear
  AddLiteral (cfa3e3b0-240c-423b-8dda-7a38ea23db00)
 Call ID: cfa3e3b0-240c-423b-8dda-7a38ea23db00
  Args:
    literal_type: xsd:string
    literal_value: 1904
    source: Maria_de_las_Mercedes
    relation: :hasDeathYear
  AddLiteral (bff5e4e8-3224-47aa-8ea8-aa6ccd118243)
 Call ID: bff5e4e8-3224-47aa-8ea8-aa6ccd118243
  Args:
    literal_type: xsd:string
    literal_value: 1901
    source: Maria_de_las_Mercedes
    relation: :hasMarriageYear
  Finish (d9c52b19-22bd-460a-b15b-ea0c3307e06b)
 Call ID: d9c52b19-22bd-460a-b15b-ea0c3307e06b
  Args: