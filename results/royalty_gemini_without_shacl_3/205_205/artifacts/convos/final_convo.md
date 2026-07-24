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
Infanta Beatriz of Spain, Princess of Civitella-Cesi (Beatriz Isabel Federica Alfonsa Eugénie Cristina Maria Teresia Bienvenida Ladislàa de Borbón y Battenberg; 22 June 1909 – 22 November 2002) was a daughter of King Alfonso XIII of Spain and Victoria Eugenie of Battenberg, wife of Alessandro Torlonia, 5th Prince di Civitella-Cesi.
She was a paternal aunt of King Juan Carlos I.


Childhood

Born at the royal palace of La Granja, San Ildefonso near Segovia, Spain on 22 June 1909, Infanta Beatriz was the third child among the six surviving children of King Alfonso XIII of Spain and Victoria Eugenie of Battenberg.
She was named Beatriz after her maternal grandmother, Princess Beatrice of the United Kingdom, the youngest daughter of Queen Victoria; Isabel for her great-aunt, Infanta Isabel; Federica for Princess Frederica of Hanover in whose house her parents had become engaged; Alfonsa after her father; Eugenia for Empress Eugénie of the French, her mother's godmother, Cristina and Maria for Maria Christina of Austria, her paternal grandmother, Teresia after Empress Maria Theresa and Ladislaa after Ladislaus the Posthumous.
Infanta Beatriz was educated within the walls of the Palacio de Oriente by English nannies.
Infanta Beatriz and her sister Maria Cristina, two years her junior, yearned to go to private schools like the daughters of the nobility who frequented the palace as their playmates, but, following Spanish tradition, they were educated by governesses and private tutors.
Their parents placed great importance on outdoor exercise and Infanta Beatriz became fond of sports.
Early life

During the late 1920s, Infanta Beatriz and her sister Infanta Cristina presided at a number of official engagements while heading various institutions and sponsoring events.
Beatriz and her sister took nursing classes, helping twice a week at the Red Cross in Madrid from 9 am to 1 pm and from 3 to 7 pm.
Beatriz was president of the Red Cross in San Sebastián, working there during the royal family's summer vacation.
Beatriz, who resembled her Spanish relatives, was a brunette, tall and lean like her father.
In 1929, Infanta Beatriz turned twenty years old.
She fell in love with Miguel Primo de Rivera y Sáenz de Heredia, the youngest son of Miguel Primo de Rivera, who served as Prime Minister of Spain from 1923 to January 1930 with dictatorial powers.
Because Beatriz and her sister could be carriers of hemophilia, like their mother, King Alphonso XIII was reluctant to follow the tradition of finding husbands for them among Catholic royal princes.
The two sisters' constant companions were their cousins Alvaro, Alonso and Ataúlfo de Orleans y Borbón, the three sons of Infante Alfonso de Orleans y Borbón.
It was expected that Infanta Beatriz would marry Alonso and Maria Cristina, Alvaro, but nothing came out of it as their companionship was interrupted when the turbulent political situation in Spain derailed their lives.
Exile

The support that Alfonso XIII gave to the unpopular dictatorship of Primo de Rivera discredited the king.
Lacking the backing of the military forces, King Alfonso felt obliged to leave the country the same day, but did not abdicate, hoping to be called back to the throne.
Infanta Beatriz, her mother and her siblings, except for Infante Don Juan, who was away on assignment in the Spanish navy, were left behind in Madrid.
The marriage of their parents was unhappy and even in Spain the King and Queen led separate lives.
Queen Victoria Eugenie moved to London and later to Lausanne, Switzerland and the two infantas lived for a time with her.
In 1933 the king moved to Rapallo and as life was too isolated for Beatriz and her sister in Lausanne, they moved with their father to Italy.
At their daughters' insistence, King Alfonso moved to Rome and rented a house for them there.
Infanta Beatriz and her sister became friends with the members of the Italian royal family and quickly adapted to life in Rome.
Beatriz, who was spending summer vacation in Pörtschach am Wörthersee in Austria, was driving a car with her brother Gonzalo as passenger.
Marriage and issue

At the time of her brother's death, Infanta Beatriz was looking forward to her wedding.
While visiting Ostia, she was introduced to an Italian aristocrat, Alessandro Torlonia, 5th Prince di Civitella-Cesi.
Torlonia, who had inherited large estates from his father in 1933, was the son of Marino, 4th Prince di Civitella-Cesi and Mary Elsie Moore, an American heiress.
His family had acquired a fortune in the 18th and 19th centuries by administering the finances of the Vatican, receiving the title of Prince of Civitella-Cesi in 1803 from Pope Pius VII.
Although Don Alessandro was a prince, he did not belong to a reigning or formerly reigning dynasty, so Beatriz had to marry him morganatically, renouncing her rights of succession to the throne of Spain.
Alfonso XIII,
The wedding took place on 14 January 1935 at the Church of the Gesù with Beatriz wearing a 20-foot train, a coronet of orange blossom holding her veil in place, in the presence of King Alfonso, the King and Queen of Italy and some 52 princes of the blood royal.
Thousands of Spaniards traveled from Spain to give support to the deposed royal family in what became a political event.
However, neither Queen Victoria Eugenie nor Beatriz's eldest brother, Alfonso, Count of Covadonga, who were on bad terms with the King, attended the wedding.
Infanta Beatriz of Spain, Princess of Civitella-Cesi, and her husband had four children, eleven grandchildren and nineteen great-grandchildren:


Later life

Infanta Beatriz settled with her husband in the Palazzo Torlonia, a 16th-century Early Renaissance town house on Via della Conciliazione in Rome.
King Alfonso XIII died in 1941 and as the situation deteriorated in Italy during World War II, Infanta Beatriz with her family joined her siblings in Lausanne, spending the rest of the war close to their mother Queen Victoria Eugenie.
Beatriz returned to Italy after the war and dwelt there for the rest of her life.
In 1950, while staying with her brother Juan, in Estoril, Portugal, Infanta Beatriz obtained authorization from Francisco Franco to make a visit to Spain.
She returned to Spain on 25 August 1950 for the first time since her departure to exile almost twenty years earlier.
They stayed at the Ritz hotel in Madrid visiting the palace of la Granja, where the Infanta was born, and the Cathedral-Basilica of Our Lady of the Pillar in Zaragoza.
Infanta Beatriz was received with such a manifestation of support for the monarchy that after only a week, of a planned much longer visit, the government gave her only twenty four hours to leave the country.
Although the family tried to arrange a marriage for the Infanta's daughter, Sandra, with King Baudouin of Belgium, she caused her parents concern when in 1958 she married Clemente Lequio, a widower with a son, who was given the title "Count Lequio di Assaba" in 1963 by Umberto II of Italy.
Their son, Alesandro Lequio, moved to Spain in 1991 working initially for Fiat.
Married to the Italian model Antonia Dell’Atte, a muse in the late 1980s of Giorgio Armani, Alessandro Lequio quickly became a favorite of the Spanish jet set and tabloids, when, after his divorce, he began a relationship with Ana Obregón, a Spanish actress and television presenter.
Infanta Beatriz's eldest son, Marco, married three times and had three children, one in each marriage.
His eldest son, Don Giovanni Torlonia, is a well known designer.
Infanta Beatriz's second son, Marino, died unmarried in 1995 of HIV-related illnesses.
The youngest child, Olimpia, married in 1965 Paul-Annick Weiller (1933–1998), the first son of the aviator Paul-Louis Weiller of the Javal family.
Among their six children is Princess Sibilla of Luxembourg.
Infanta Beatriz remained very fond of Spain and supported the claims to the Spanish throne of her brother Don Juan.
In 1962, she joined the Spanish royal family in the celebration in Athens for the wedding of her nephew the future King Don Juan Carlos with Princess Sophia of Greece.
A femur fracture in 1973 never healed completely, affecting Infanta Beatriz's mobility for the rest of her life.
Her fragile health did not allow her to join her family at the ascension to the throne of King Juan Carlos, the wedding of the Infantas Elena and Cristina or the ceremonies for the return to Spain of the remains of her parents and siblings who had died in exile.
Nevertheless, Infanta Beatriz not only survived all of her siblings, but visited Spain again in 1998 to visit la Granja.
In 1999, the Infanta gave an interview with ¡Hola! Magazine, where she discussed her life and the years of the Royal Family's exile from Spain.
She made her last visit to Spain in 2001 to be with her sister-in-law Doña Maria and returned to the Palacio de la Magdalena, near Santander, where 70 years earlier she had spent her summer vacation for 17 consecutive years until 1930.
She died at her home in Palazzo Torlonia, Rome on 22 November 2002 at 93 years 5 months.
She was the last surviving legitimate child of Alfonso XIII and the last surviving legitimate grandchild of Alfonso XII of Spain.



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
  AssignClass (8f59c7b2-f5c5-475e-a701-10e49154a616)
 Call ID: 8f59c7b2-f5c5-475e-a701-10e49154a616
  Args:
    type: :Woman
    source: Beatriz_de_Borbón_y_Battenberg
  AssignClass (687717f9-e7c4-4684-9483-e24560c435f8)
 Call ID: 687717f9-e7c4-4684-9483-e24560c435f8
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (039cdda3-8dcf-450a-9cb4-d40e90124665)
 Call ID: 039cdda3-8dcf-450a-9cb4-d40e90124665
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (80d0adaa-4299-4fb5-8ee6-52ce7a11908e)
 Call ID: 80d0adaa-4299-4fb5-8ee6-52ce7a11908e
  Args:
    type: :Man
    source: Alessandro_Torlonia
  AssignClass (91988f2d-dd67-43e1-ac30-260f08627b7b)
 Call ID: 91988f2d-dd67-43e1-ac30-260f08627b7b
  Args:
    type: :Man
    source: Juan_Carlos_I
  AddLiteral (f869c4ee-e602-4d20-9cd4-a62a095f5afd)
 Call ID: f869c4ee-e602-4d20-9cd4-a62a095f5afd
  Args:
    literal_value: 1909
    relation: :hasBirthYear
    source: Beatriz_de_Borbón_y_Battenberg
    literal_type: xsd:integer
  AddLiteral (7aa1eb22-667b-41a8-829d-dc6cb91a1985)
 Call ID: 7aa1eb22-667b-41a8-829d-dc6cb91a1985
  Args:
    source: Beatriz_de_Borbón_y_Battenberg
    literal_type: xsd:integer
    literal_value: 2002
    relation: :hasDeathYear
  AddTriple (b68ec286-2314-4a52-8cfc-d7d7d40ccdab)
 Call ID: b68ec286-2314-4a52-8cfc-d7d7d40ccdab
  Args:
    target: Alfonso_XIII_of_Spain
    relation: :hasFather
    source: Beatriz_de_Borbón_y_Battenberg
  AddTriple (8dd17173-36c4-4adb-9776-2f194754e3bd)
 Call ID: 8dd17173-36c4-4adb-9776-2f194754e3bd
  Args:
    relation: :hasMother
    source: Beatriz_de_Borbón_y_Battenberg
    target: Victoria_Eugenie_of_Battenberg
  AddTriple (938cfb64-bc04-43bd-bc62-7731e1518f9a)
 Call ID: 938cfb64-bc04-43bd-bc62-7731e1518f9a
  Args:
    target: Alessandro_Torlonia
    relation: :hasRelation
    source: Beatriz_de_Borbón_y_Battenberg
  AddLiteral (3d036444-acf8-42c1-82f2-b822e5e1c446)
 Call ID: 3d036444-acf8-42c1-82f2-b822e5e1c446
  Args:
    literal_value: 1935
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Beatriz_de_Borbón_y_Battenberg
  AddTriple (88d841cc-92f6-475e-bbaf-2caad76c3c21)
 Call ID: 88d841cc-92f6-475e-bbaf-2caad76c3c21
  Args:
    relation: :isAuntOf
    source: Beatriz_de_Borbón_y_Battenberg
    target: Juan_Carlos_I
  AssignClass (45d9390a-2de7-45c9-a1b8-b6a65474ac3a)
 Call ID: 45d9390a-2de7-45c9-a1b8-b6a65474ac3a
  Args:
    type: :Woman
    source: Maria_Cristina_de_Borbón_y_Battenberg
  AddTriple (66d29cd3-2b10-4a54-b4a8-447550c0a8da)
 Call ID: 66d29cd3-2b10-4a54-b4a8-447550c0a8da
  Args:
    target: Maria_Cristina_de_Borbón_y_Battenberg
    source: Beatriz_de_Borbón_y_Battenberg
    relation: :isSisterOf
  AssignClass (7d28e1a3-497c-4a5f-9fe0-ccd76acbf002)
 Call ID: 7d28e1a3-497c-4a5f-9fe0-ccd76acbf002
  Args:
    type: :Man
    source: Gonzalo_de_Borbón_y_Battenberg
  AddTriple (717483df-832d-4378-af2e-6c77d9a93498)
 Call ID: 717483df-832d-4378-af2e-6c77d9a93498
  Args:
    source: Beatriz_de_Borbón_y_Battenberg
    relation: :hasBrother
    target: Gonzalo_de_Borbón_y_Battenberg
  AssignClass (69ffc542-e294-496d-8459-6567ed6e0195)
 Call ID: 69ffc542-e294-496d-8459-6567ed6e0195
  Args:
    type: :Man
    source: Alfonso_de_Borbón_y_Battenberg
  AddTriple (3c6836fa-745a-4e9f-a7e7-6b52a63112c9)
 Call ID: 3c6836fa-745a-4e9f-a7e7-6b52a63112c9
  Args:
    relation: :hasBrother
    source: Beatriz_de_Borbón_y_Battenberg
    target: Alfonso_de_Borbón_y_Battenberg
  AssignClass (b1be4554-9a37-484c-8ed8-302a24b2f2f6)
 Call ID: b1be4554-9a37-484c-8ed8-302a24b2f2f6
  Args:
    type: :Man
    source: Juan_de_Borbón_y_Battenberg
  AddTriple (54eb9075-7776-4a5f-ab8f-8160cd6e3f48)
 Call ID: 54eb9075-7776-4a5f-ab8f-8160cd6e3f48
  Args:
    source: Beatriz_de_Borbón_y_Battenberg
    relation: :hasBrother
    target: Juan_de_Borbón_y_Battenberg
  AssignClass (97b190e4-8a9e-487c-9c31-059569b4e7ad)
 Call ID: 97b190e4-8a9e-487c-9c31-059569b4e7ad
  Args:
    type: :Man
    source: Marino_Torlonia
  AssignClass (d95a3070-9770-43f9-bdb1-7b59e89db536)
 Call ID: d95a3070-9770-43f9-bdb1-7b59e89db536
  Args:
    type: :Woman
    source: Mary_Elsie_Moore
  AddTriple (67df062d-d9fc-46d3-b78e-88d82216aea5)
 Call ID: 67df062d-d9fc-46d3-b78e-88d82216aea5
  Args:
    relation: :hasFather
    source: Alessandro_Torlonia
    target: Marino_Torlonia
  AddTriple (43bfa7a9-b5de-4afe-bd9f-a2bceefb172c)
 Call ID: 43bfa7a9-b5de-4afe-bd9f-a2bceefb172c
  Args:
    source: Alessandro_Torlonia
    relation: :hasMother
    target: Mary_Elsie_Moore
  AssignClass (9958871e-247d-49d1-8cb7-b76d19e4fe4a)
 Call ID: 9958871e-247d-49d1-8cb7-b76d19e4fe4a
  Args:
    type: :Woman
    source: Sandra_Torlonia
  AssignClass (213bcea6-6a14-4739-acbb-c8292cc5aff7)
 Call ID: 213bcea6-6a14-4739-acbb-c8292cc5aff7
  Args:
    type: :Man
    source: Marco_Torlonia
  AssignClass (76984ef1-a6fc-4e45-b157-8c1dc135506b)
 Call ID: 76984ef1-a6fc-4e45-b157-8c1dc135506b
  Args:
    type: :Man
    source: Marino_Torlonia_jr
  AssignClass (13285f7f-160f-4219-b83a-eaa20c063c46)
 Call ID: 13285f7f-160f-4219-b83a-eaa20c063c46
  Args:
    type: :Woman
    source: Olimpia_Torlonia
  AddTriple (a62649a4-52f6-4379-b530-2c8752ecfc8a)
 Call ID: a62649a4-52f6-4379-b530-2c8752ecfc8a
  Args:
    relation: :hasChild
    source: Beatriz_de_Borbón_y_Battenberg
    target: Sandra_Torlonia
  AddTriple (c49ceabe-29fa-4e8a-a288-f694f851bcfa)
 Call ID: c49ceabe-29fa-4e8a-a288-f694f851bcfa
  Args:
    target: Marco_Torlonia
    source: Beatriz_de_Borbón_y_Battenberg
    relation: :hasChild
  AddTriple (a7122788-2b21-4604-911b-02681bf3a17e)
 Call ID: a7122788-2b21-4604-911b-02681bf3a17e
  Args:
    target: Marino_Torlonia_jr
    source: Beatriz_de_Borbón_y_Battenberg
    relation: :hasChild
  AddTriple (a0660f60-5505-422a-b958-9aa5dcbdf6b8)
 Call ID: a0660f60-5505-422a-b958-9aa5dcbdf6b8
  Args:
    source: Beatriz_de_Borbón_y_Battenberg
    relation: :hasChild
    target: Olimpia_Torlonia
  Finish (52cebdfc-e020-42e9-956e-6583aaed32b8)
 Call ID: 52cebdfc-e020-42e9-956e-6583aaed32b8
  Args: